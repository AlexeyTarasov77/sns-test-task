"use client"
import { useUserCtx } from "@/entity/users/context/user"
import { Loader } from "@/shared/ui/loader"
import { useListChats } from "./api/chats"
import Image from "next/image"
import { useState } from "react"
import { Avatar } from "@/shared/avatar"

export function ChatsListPage() {
  const { user, isLoading: isUserLoading } = useUserCtx()
  const { chats, isLoading: isChatsLoading } = useListChats(!!user?.tg)
  const [searchQuery, setSearchQuery] = useState("")
  if (isUserLoading || isChatsLoading) return <Loader />
  if (!user?.tg) {
    return <h1 className="text-center text-3xl mt-5 font-bold font-mono">You don't have telegram account connected yet. Connect it to view chats list</h1>
  }
  const filteredChats = searchQuery ? chats.filter(chat => chat.title.toLowerCase().includes(searchQuery.toLowerCase())) : chats
  return (
    <div className="px-40 flex flex-1 justify-center py-5">
      <div className="layout-content-container flex flex-col max-w-[960px] flex-1">
        <div className="px-4 py-3">
          <label className="flex flex-col min-w-40 h-12 w-full">
            <div className="flex w-full flex-1 items-stretch rounded-lg h-full">
              <div
                className="text-[#60758a] flex border-none bg-[#f0f2f5] items-center justify-center pl-4 rounded-l-lg border-r-0"
                data-icon="MagnifyingGlass"
                data-size="24px"
                data-weight="regular"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor" viewBox="0 0 256 256">
                  <path
                    d="M229.66,218.34l-50.07-50.06a88.11,88.11,0,1,0-11.31,11.31l50.06,50.07a8,8,0,0,0,11.32-11.32ZM40,112a72,72,0,1,1,72,72A72.08,72.08,0,0,1,40,112Z"
                  ></path>
                </svg>
              </div>
              <input
                placeholder="Search chats"
                className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#111418] focus:outline-0 focus:ring-0 border-none bg-[#f0f2f5] focus:border-none h-full placeholder:text-[#60758a] px-4 rounded-l-none border-l-0 pl-2 text-base font-normal leading-normal"
                onChange={(e) => setSearchQuery(e.target.value)}
                value={searchQuery}
              />
            </div>
          </label>
        </div>
        {filteredChats.map(chat => (
          <div key={chat.id} className="flex items-center gap-4 bg-white px-4 min-h-[72px] py-2">
            <Avatar
              src={chat.photo_url}
              size={50}
            ></Avatar>
            <div className="flex flex-col justify-center">
              <p className="text-[#111418] text-base font-medium leading-normal line-clamp-1">{chat.title}</p>
              <p className="text-[#60758a] text-sm font-normal leading-normal line-clamp-2">{chat.last_message}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
