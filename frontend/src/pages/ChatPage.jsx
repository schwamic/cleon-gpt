import { ReadyState } from 'react-use-websocket';
import { useRef, useEffect } from 'react'

import { useGetUser } from '/src/modules/common/clients/useCleonApi';
import { Frame } from '/src/modules/common/ui-components';
import { ChatHeader, ChatMessageInput, ChatConversations } from '/src/modules/chat/components';
import { useChat } from '/src/modules/chat/hooks';
import content from '/src/assets/content.json';


const USER_ID = "088948cc-e508-4ead-afde-7b9dd013a940"
const CHAT_ID = "579d6fb7-fa62-42bd-80bb-7f4870cbd810"


/**
 * Main Chat Page (View Layer)
 */
function ChatPage() {
    const { data: user } = useGetUser(USER_ID)
    const [chatHistory, messageHistory, handleClickSendMessage, readyState, isDirty, settingOptions, currentSettings] = useChat(CHAT_ID)
    const scrollContainerRef = useRef(null);

    useEffect(() => {
        if (!scrollContainerRef.current) {
            return;
        }
        scrollContainerRef.current.scrollTop = scrollContainerRef.current.scrollHeight;
    }, [messageHistory, chatHistory]);

    return (
        <Frame className="flex flex-col">
            <div>
                <ChatHeader
                    settings={settingOptions}
                    currentSettings={currentSettings}
                    onSettingsChange={handleClickSendMessage}
                    nickname={user?.nickname}
                    isOnline={readyState === ReadyState.OPEN} />
            </div>
            <div className="grow overflow-y-scroll h-0" ref={scrollContainerRef}>
                {isDirty ?
                    <ChatConversations
                        chatHistory={chatHistory}
                        messageHistory={messageHistory.join("")} />
                    : <div className="text-center mt-20">
                        <h2 className="italic font-black text-3xl mb-6">{content.title}</h2>
                        <h2 className="italic font-black text-lg">{content.welcome_message}</h2>
                    </div>
                }
            </div>
            <div className="mt-3">
                <ChatMessageInput
                    disabled={readyState !== ReadyState.OPEN}
                    onClick={handleClickSendMessage} />
            </div>
        </Frame>
    );
}

export default ChatPage
