// chat_room.mjs
class ChatRoom {
  constructor() {
    this.isExpanded = false;
    this.isSecondaryOpen = false;
    this.chatRoom = document.getElementById("chat-room");
    this.setupButtons();
  }

  setupButtons() {
    // Expand button
    const expandButton = document.getElementById("chat-room-expand-button");
    expandButton.addEventListener("click", () => this.toggleExpand());

    // Close button
    const closeButton = document.getElementById("chat-room-close-button");
    closeButton.addEventListener("click", () => this.closeChat());

    // Plus/Minus button
    const plusButton = document.getElementById("chat-room-plus-button");
    plusButton.addEventListener("click", () => this.toggleSecondary());
  }

  toggleExpand() {
    console.log("Toggle Expand");
    const button = document.getElementById("chat-room-expand-button");
    this.isExpanded = !this.isExpanded;

    if (this.isExpanded) {
      this.chatRoom.classList.remove("chat-room-md");
      this.chatRoom.classList.add("chat-room-lg");
      button.textContent = "<";
    } else {
      this.chatRoom.classList.add("chat-room-md");
      this.chatRoom.classList.remove("chat-room-lg");
      button.textContent = ">";
    }
  }

  closeChat() {
    console.log("Close Chat");
    this.chatRoom.classList.add("sb-hidden");
    // Add your reopen button logic here
    this.addReopenButton();
  }

  addReopenButton() {
    const reopenButton = document.createElement("button");
    reopenButton.textContent = "Open Chat";
    reopenButton.className =
      "sb-fixed sb-bottom-0 sb-right-4 sb-bg-primary sb-text-white sb-px-4 sb-py-2 sb-rounded";
    reopenButton.addEventListener("click", () => {
      this.chatRoom.classList.remove("sb-hidden");
      reopenButton.remove();
    });
    document.body.appendChild(reopenButton);
  }

  toggleSecondary() {
    const button = document.getElementById("chat-room-plus-button");
    this.isSecondaryOpen = !this.isSecondaryOpen;

    if (this.isSecondaryOpen) {
      this.createSecondaryChat();
      button.textContent = "-";
    } else {
      this.removeSecondaryChat();
      button.textContent = "+";
    }
  }

  createSecondaryChat() {
    // Create secondary chat window logic
    console.log("Create Secondary Chat");
  }

  removeSecondaryChat() {
    const secondaryChat = document.getElementById("secondary-chat-room");
    if (secondaryChat) {
      secondaryChat.remove();
    }
  }
}

// after HTMX loads, create the chat room
document.addEventListener("htmx:afterSettle", (event) => {
  // check if the settled element is the chat room
  if (event.target.id !== "chat-room") {
    return;
  }
  const chatRoom = new ChatRoom();
  console.log("Chat Room Created");
});
export default ChatRoom;
