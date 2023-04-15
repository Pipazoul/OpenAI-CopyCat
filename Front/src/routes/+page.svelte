<script lang="ts">
	import { onMount } from "svelte";
    import { PUBLIC_WS_URL } from '$env/static/public';

    let pastMessage: Array = [
        {content: "Hello I am a conversation assistant, I am here to help you and answer your problems what can I do for you?", sender: "ai"},
    ]
    let userMsg = ""

    onMount(async () => {
        // get the past message from the local storage
        let pastMessageStorage = localStorage.getItem("pastMessage")
        if (pastMessageStorage) {
            pastMessage = JSON.parse(pastMessageStorage)
        }
    })

    function sendMsg(e) {
        if (e.key === "Enter") {
          
            const params = {
                temperature: 1.5,
                num_tokens: 300,
                stop_word: "<|assistant|>, <|prompter|>",
                top_p: 1.0,
                repetition_p: 1.0,
            };

            let ws = new WebSocket(PUBLIC_WS_URL);

            
            ws.onopen = function (e) {
                console.log("Connection established!");
                pastMessage = [...pastMessage, {content: userMsg, sender: "human"}]
                userMsg = ""
                console.log(pastMessage)

                // request message take avery message on the pastMessage array and send it to the api AI: msg \n HUMAN: msg
                let requestMessage = ""
                pastMessage.forEach((msg) => {
                    if (msg.sender === "human") {
                        requestMessage = requestMessage + "<|prompter|>" + msg.content + "\n"
                    } else {
                        requestMessage = requestMessage + "<|assistant|>" + msg.content + "\n"
                    }
                })
                console.log("requets message",requestMessage)
                requestMessage = requestMessage + "<|assistant|>"

                const msg = {
                    params: JSON.stringify(params),
                    text: requestMessage
                };

                //send text to websocket
                ws.send(JSON.stringify(msg));
                
                // append empty message to the pastMessage array
                pastMessage = [...pastMessage, {content: "", sender: "ai"}]

                // wait for response
                let buffer = ""
                ws.onmessage = function (e) {
                    console.log("Message from server ", e.data);
                    // update the last message with the response but keep last content
                    buffer=buffer+e.data
                    pastMessage[pastMessage.length-1].content = buffer
                    
                };   

                // save all the past message in the local storage
                localStorage.setItem("pastMessage", JSON.stringify(pastMessage))
            };

        }
        
    }

    function clearPastMessage() {
        pastMessage = [
            {content: "Hello I am a conversation assistant, I am here to help you and answer your problems what can I do for you?", sender: "ai"},
        ]
        localStorage.setItem("pastMessage", JSON.stringify(pastMessage))
    }


</script>
<section class="flex lg:flex-row h-screen flex-col">
    <div class="bg-slate-800 text-white lg:w-2/12">
        <ul>
            <li>New Chat</li>
            <li on:click={() => {clearPastMessage()}}>Clear Chat</li>
        </ul>
    </div>
    <div class="lg:w-10/12 bg-gray-400 h-screen">
        <div class="flex flex-col h-5/6">
            {#each pastMessage as msg}
                <div class="bg-white rounded-lg p-2 m-2">
                    {msg.content}
                </div>
            {/each}
        <input type="text" placeholder="Write message here" on:keydown={(e) => {sendMsg(e) }} bind:value={userMsg}/>
    </div>
</section>