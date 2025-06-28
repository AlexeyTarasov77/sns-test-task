import { IChat } from "@/entity/chats/types";
import { Avatar } from "@/shared/avatar";
import { useRouter } from "next/navigation";

export function ChatItem({ chat }: { chat: IChat }) {
  const router = useRouter()
  return (
    <div onClick={() => router.push("/chats/" + String(chat.id))} className="flex items-center gap-4 bg-white px-4 min-h-[72px] py-2 transition-colors hover:bg-blue-300">
      <Avatar
        src={chat.photo_url}
        size={50}
      ></Avatar>
      <div className="flex flex-col justify-center">
        <p className="text-[#111418] text-base font-medium leading-normal line-clamp-1">{chat.title}</p>
        <p className="text-[#60758a] text-sm font-normal leading-normal line-clamp-2">{chat.last_message}</p>
      </div>
    </div>
  )
}
