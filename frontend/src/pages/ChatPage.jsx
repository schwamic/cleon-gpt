import { useState, useCallback, useEffect } from 'react';
import { ReadyState } from 'react-use-websocket';

import { useConversationSocket, useGetUser } from '/src/modules/common/clients/useCleonApi';


const CHAT_ID = "579d6fb7-fa62-42bd-80bb-7f4870cbd810"
const USER_ID = "088948cc-e508-4ead-afde-7b9dd013a940"

function ChatPage() {
    const { data: user } = useGetUser(USER_ID)
    const [messageHistory, setMessageHistory] = useState([]);
    const [chatHistory, setChatHistory] = useState([]);
    const { sendMessage, lastMessage, readyState } = useConversationSocket(CHAT_ID);

    useEffect(() => {
        if (lastMessage !== null) {
            const event = JSON.parse(lastMessage.data)
            if (event?.type == "status") {
                console.log("status", event)
                const message = messageHistory.join("")
                setChatHistory((prev) => prev.concat({ type: "ai_message", content: message }));
                setMessageHistory([]);
            } else {
                const message = event?.data?.message
                setMessageHistory((prev) => prev.concat(message));
            }
        }
    }, [lastMessage]);

    const handleClickSendMessage = useCallback(() => {
        //const prompt = "How is the weather in 86159 Augsburg?"
        // const prompt = "Count from 1 to 3."
        const prompt = "Tell a joke in 3 words."
        setChatHistory((prev) => prev.concat({ type: "human_message", content: prompt }));
        const message = {
            type: "human_message",
            data: {
                message: prompt
            }
        }
        sendMessage(JSON.stringify(message))

    }, [sendMessage]);

    const connectionStatus = {
        [ReadyState.CONNECTING]: 'Connecting',
        [ReadyState.OPEN]: 'Open',
        [ReadyState.CLOSING]: 'Closing',
        [ReadyState.CLOSED]: 'Closed',
        [ReadyState.UNINSTANTIATED]: 'Uninstantiated',
    }[readyState];

    return (
        <>
            <h1>Cleon GPT</h1>
            <div>
                <button
                    onClick={handleClickSendMessage}
                    disabled={readyState !== ReadyState.OPEN}
                >
                    SEND MESSAGE
                </button>
            </div>
            <div>The WebSocket is currently {connectionStatus}</div>
            {lastMessage ? <div>Last message: {lastMessage.data}</div> : null}
            {user ? <div>Active User: {user.nickname} – {user.id}</div> : null}
            {chatHistory?.map((message, idx) => <div key={idx}>{message?.type + ": " + message?.content}</div>)}
            <div>{messageHistory.join("")}</div>
        </>
    );
}

export default ChatPage
