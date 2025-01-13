// chat_room.mjs
class ChatRoom {
  constructor() {
    this.isExpanded = false;
    this.isSecondaryOpen = false;
    this.chatRoom = document.getElementById("chat-room");
    this.setupButtons();
  }

  setupButtons() {
    console.log(`Chat Room: ${this.chatRoom}`);
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
    const button = document.getElementById("chat-room-expand-button");
    this.isExpanded = !this.isExpanded;

    if (this.isExpanded) {
      this.chatRoom.classList.add("sb-w-96"); // or whatever width class you want
      this.chatRoom.classList.remove("sb-w-64"); // default width
      button.textContent = "<";
    } else {
      this.chatRoom.classList.remove("sb-w-96");
      this.chatRoom.classList.add("sb-w-64");
      button.textContent = ">";
    }
  }

  closeChat() {
    this.chatRoom.classList.add("sb-hidden");
    // Add your reopen button logic here
    this.addReopenButton();
  }

  addReopenButton() {
    const reopenButton = document.createElement("button");
    reopenButton.textContent = "Open Chat";
    reopenButton.className =
      "sb-fixed sb-bottom-4 sb-right-4 sb-bg-primary sb-text-white sb-px-4 sb-py-2 sb-rounded";
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
    const secondaryChat = this.chatRoom.cloneNode(true);
    secondaryChat.id = "secondary-chat-room";
    secondaryChat.classList.add("sb-mt-4"); // Add margin top
    this.chatRoom.parentNode.insertBefore(secondaryChat, this.chatRoom);
  }

  removeSecondaryChat() {
    const secondaryChat = document.getElementById("secondary-chat-room");
    if (secondaryChat) {
      secondaryChat.remove();
    }
  }
}

// Initialize when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  console.log("Chat Room JS Loaded");
  const chatRoom = new ChatRoom();
});

export default ChatRoom;
