import { useQuery, useMutation } from 'react-query'
import useWebSocket from 'react-use-websocket';

import { query, mutate } from '/src/modules/common/utils/requests'


const HTTP_API_V1_URL = "http://127.0.0.1:8000/api/v1";
const WS_API_V1_URL = "ws://127.0.0.1:8000/ws/api/v1";

/**
 * WS(s) hooks
 */

export function useConversationSocket(conversationId) {
    return useWebSocket(`${WS_API_V1_URL}/conversations/${conversationId}`);
};

/**
 * HTTP(s) hooks
 */

export function useGetUser(userId) {
    return useQuery(['user', userId], async () => {
        return query(`${HTTP_API_V1_URL}/users/${userId}`);
    });
}

export function useGetConversation(chatId) {
    return useQuery(['conversations', chatId], async () => {
        return query(`${HTTP_API_V1_URL}/conversations/${chatId}`);
    });
}

export function useListConfigurationOptions() {
    return useQuery({
        queryKey: ['chatConfiguration'],
        queryFn: () => mutate(`${HTTP_API_V1_URL}/conversations/:list_configuration_options`, {}),
        initialData: { models: [], temperatures: [] },
    });
}

export function useCreateConversation(payload) {
    return useMutation(async () => {
        return mutate(
            `${HTTP_API_V1_URL}/conversations`,
            {
                "user_id": payload.userId,
                "configuration": {
                    "temperature": payload.configuration.temperature
                },
                "model": payload.model,
            }
        );
    });
}
