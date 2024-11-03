import { QueryClient, QueryClientProvider } from 'react-query'
import ChatPage from '/src/pages/ChatPage'

const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ChatPage />
    </QueryClientProvider>
  );
}

export default App
