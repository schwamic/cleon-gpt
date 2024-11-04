import { useQuery, useMutation } from 'react-query'
import useWebSocket from 'react-use-websocket';

import { query, mutate } from '/src/modules/common/utils/requests'


const HTTP_API_V1_URL = import.meta.env.VITE_HTTP_API_V1_URL;
const WS_API_V1_URL = import.meta.env.VITE_WS_API_V1_URL;


/**
 * Client for Cleon API
 * - WS(s) hooks
 * - HTTP(s) hooks
 */

export function useConversationSocket(conversationId) {
    return useWebSocket(`${WS_API_V1_URL}/conversations/${conversationId}`);
};

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
