import { useState, useCallback, useEffect } from 'react';
import useWebSocket, { ReadyState } from 'react-use-websocket';
import './App.css'

const WEB_SOCKET_URL = "ws://127.0.0.1:8000/ws/api/v1/conversations";
const ID = "1a99a183-808c-4918-855a-93baff9b371b"

function App() {
  const [socketUrl, setSocketUrl] = useState(`${WEB_SOCKET_URL}/${ID}`);
  const [messageHistory, setMessageHistory] = useState([]);
  const { sendMessage, lastMessage, readyState } = useWebSocket(`${WEB_SOCKET_URL}/${ID}`);

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

export default App
