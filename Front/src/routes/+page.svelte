<script lang="ts">
	import { onMount } from "svelte";


    let apiUrl = "http://178.116.94.163:38001"

    let pastMessage: Array = [
        {content: "Hello I am a conversation assistant, I am here to help you and answer your problems what can I do for you?", sender: "ai"},
    ]
    let userMsg = ""
    
    // bloom params topk top p temperature token
    let bloomParams = [4000, 1, 50, 0.5]

    onMount(async () => {

    })


    function sendMsg(e) {
        console.log(e.key)
        if (e.key === "Enter") {
            pastMessage = [...pastMessage, {content: userMsg, sender: "human"}]
            userMsg = ""
            console.log(pastMessage)

            // request message take avery message on the pastMessage array and send it to the api AI: msg \n HUMAN: msg
            let requestMessage = ""
            pastMessage.forEach((msg) => {
                if (msg.sender === "human") {
                    requestMessage = requestMessage + "HUMAN: " + msg.content + "\n"
                } else {
                    requestMessage = requestMessage + "AI: " + msg.content + "\n"
                }
            })
            console.log("requets message",requestMessage)
            requestMessage = requestMessage + "AI: "
            // fetch post route with data array [ userMsg, 30, 1, 50, 0.50 ]
            fetch(apiUrl + "/bloomz/run/predict" , {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    "data": [requestMessage, 4000, 1, 50, 0.5]
                })
            })
            .then(res => res.json())
            .then(data => {
                console.log(data)

                // extact the last message from the response and add it to the pastMessage array for ex Salut I'm your AI
                let endToText = data.data[0].split("\n").pop().split("AI: ").pop()

                console.log(endToText)
                pastMessage = [...pastMessage, {content: endToText, sender: "ai"}]

            })
        }
    }

</script>
<section class="flex lg:flex-row h-screen flex-col">
    <div class="bg-slate-800 text-white lg:w-2/12">
        <ul>
            <li>New Chat</li>
            <li>LOL</li>
            <li><input bind:value={apiUrl} class="text-black w-full"></li>
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