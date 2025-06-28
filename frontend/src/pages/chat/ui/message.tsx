import { IChatMessage } from "@/entity/chats/types";
import { Avatar } from "@/shared/avatar";

export function Message({ msg }: { msg: IChatMessage }) {
  const isOutgoing = msg.out;

  return (
    <div className={`flex items-end gap-3 p-4 ${isOutgoing ? "justify-end" : ""}`}>
      {!isOutgoing && <Avatar src={msg.sender.photo_url} size={40} />}
      <div className={`flex flex-1 flex-col gap-1 ${isOutgoing ? "items-end" : "items-start"}`}>
        <p
          className={`text-[#60758a] text-[13px] font-normal leading-normal max-w-[360px] ${isOutgoing ? "text-right" : ""}`}
        >
          {isOutgoing ? "You" : msg.sender.display_name}
        </p>
        <p
          className={`text-base font-normal leading-normal flex max-w-[360px] rounded-lg px-4 py-3 ${isOutgoing ? "bg-[#0c7ff2] text-white" : "bg-[#f0f2f5] text-[#111418]"
            }`}
        >
          {msg.message}
        </p>
      </div>
      {isOutgoing && <Avatar src={msg.sender.photo_url} size={40} />}
    </div>
  );
}

