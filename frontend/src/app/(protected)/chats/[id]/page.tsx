import { ChatPage } from "@/pages/chat/page"

export default async function Page({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params

  return <ChatPage chatId={Number(id)} />
}
