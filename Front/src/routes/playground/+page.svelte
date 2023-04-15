<script lang="ts">
    import { quill } from "svelte-quill";
	import { bind, text } from "svelte/internal";
    import { PUBLIC_WS_URL } from '$env/static/public';

    let temperature: number = 0.5;
    let max_length: number = 100;
    let stop_sequence = ["\n"];
    let top_p: number = 1;
    let frequency_penalty: number = 0;
    let presence_penalty: number = 0;
    let best_of: number = 1;

    let content;
    let messages = "";

    $: {
        if (content) {
            console.log(content.text);
            messages = content.text;
        }
    }

    function sendMsg() {
          
        const params = {
            temperature,
            max_length,
            stop_sequence,
            top_p,
            frequency_penalty,
            presence_penalty,
            best_of,
        };

            let ws = new WebSocket("ws://" + PUBLIC_WS_URL);

            
            ws.onopen = function (e) {
                console.log("Connection established!");
  
                const msg = {
                    params: JSON.stringify(params),
                    text: content.text
                };
                ws.send(JSON.stringify(msg));
                // wait for response and add message to the same pastMessage array index
                

                // wait for response
                let buffer = ""
                ws.onmessage = function (e) {
                    console.log("Message from server ", e.data);
                    // update the last message with the response but keep last content
                    messages = messages + e.data;
                };
               
               
            };

        
        
    }
    
 
    const options = {
        modules: {
            toolbar: false,
        },
        placeholder: "Type something...",
        theme: "snow"
    }


</script>
<section class="flex flex-row h-auto">
    <div class="w-1/6">
        <h1>Get started</h1>
        <p>
            Enter an instruction or select a preset, and watch the API respond with a completion that attempts to match the context or pattern you provided.
        </p>
        <p>
            You can control which model completes your request by changing the model.
        </p>
        <p>
            KEEP IN MIND
            Use good judgment when sharing outputs, and attribute them to your name or company. Learn more.
            Requests submitted to our API will not be used to train or improve future models. Learn more.
            Our default models' training data cuts off in 2021, so they may not have knowledge of current events.
        </p>
    </div>
    <div class="w-5/6">
        <div>
            <h1>Playground</h1>
            <select>
                <option>Select a preset</option>
                <option>Model 1</option>
                <option>Model 2</option>
                <option>Model 3</option>
            </select>
            <button>Save</button>
            <button>View Code</button>
        </div>
        <div class="flex">
            <div class="flex flex-col w-full">
                <div class="editor w-full h-auto" use:quill={options} on:text-change={e => content = e.detail} />
                <input type="text" bind:value={messages} />
                
                <button on:click={sendMsg}>Send</button>
            </div>

            <div>
                <p>Mode</p>
                <select>
                    <option>Complete</option>
                    <option>Chat</option>
                    <option>Insert</option>
                    <option>Edit</option>
                </select>
                <div class="flex space-x-4">
                    <p>Temperature</p>
                    <p>{temperature}</p>
                </div>
                <input type="range" min="0" max="1" step="0.1" bind:value={temperature} />
                <div class="flex space-x-4">
                    <p>Max Length</p>
                    <p>{max_length}</p>
                </div>
                <input type="range" min="0" max="1000" step="100" bind:value={max_length} />
                <div class="flex space-x-4">
                    <p>Stop Sequence</p>
                    <p></p>
                </div>
                <input type="text" />
                <div class="flex space-x-4">
                    <p>Top P</p>
                    <p>{top_p}</p>
                </div>
                <input type="range" min="0" max="1" step="0.1" bind:value={top_p} />
                <div class="flex space-x-4">
                    <p>Frequency Penalty</p>
                    <p>{frequency_penalty}</p>
                </div>
                <input type="range" min="0" max="2" step="0.1" bind:value={frequency_penalty} />
                <div class="flex space-x-4">
                    <p>Presence Penalty</p>
                    <p>{presence_penalty}</p>
                </div>
                <input type="range" min="0" max="2" step="0.1" bind:value={presence_penalty} />
                <div class="flex space-x-4">
                    <p>Best Of</p>
                    <p>{best_of}</p>
                </div>
                <input type="range" min="0" max="20" step="1" bind:value={best_of} />
                <p>Inject Start text</p>
                <input type="text" />
                <p>Inject Restart text</p>
                <input type="text" />
            </div>
        </div>
    </div>
 
</section>