import { useState, useCallback, useEffect } from 'react';
import { ReadyState } from 'react-use-websocket';

import { useConversationSocket, useGetUser } from '/src/modules/common/clients/useCleonApi';


const CHAT_ID = "1a99a183-808c-4918-855a-93baff9b371b"
const USER_ID = "088948cc-e508-4ead-afde-7b9dd013a940"

function ChatPage() {
    const { data: user } = useGetUser(USER_ID)
    const [messageHistory, setMessageHistory] = useState([]);
    const { sendMessage, lastMessage, readyState } = useConversationSocket(CHAT_ID);

    useEffect(() => {
        if (lastMessage !== null) {
            setMessageHistory((prev) => prev.concat(lastMessage));
        }
    }, [lastMessage]);


    const handleClickSendMessage = useCallback(() => {
        var message = {
            type: "message",
            data: "HELLO"
        }
        console.log("sendMessage", message)
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
                    Click Me to send HELLO
                </button>
            </div>
            <div>The WebSocket is currently {connectionStatus}</div>
            {lastMessage ? <div>Last message: {lastMessage.data}</div> : null}
            {user ? <div>Active User: {user.nickname} – {user.id}</div> : null}
            <div>
                <ul>
                    {messageHistory.map((message, idx) => (
                        <span key={idx}>{message ? message.data : null}</span>
                    ))}
                </ul>
            </div>
        </>
    );
}

export default ChatPage
