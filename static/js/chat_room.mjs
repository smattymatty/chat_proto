// chat_room.mjs
const DEBUG = true;
if (DEBUG) {
  console.log("Chat Room JS Initialized");
}

class ChatRoom {
  constructor() {
    this.expansionLevel = 0;
    this.isSecondaryOpen = false;
    this.transitionDuration = 0.25;
    this.transitionStyle = "ease-in-out";
    this.chatRoom = document.getElementById("chat-room");
    this.setupButtons();
    this.setupStyles();
  }

  setupStyles() {
    this.chatRoom.style.transition = `all ${this.transitionDuration}s ${this.transitionStyle}`;

    this.chatRoom.style.width = "30%";
    const header = document.getElementById("chat-room-header");
    for (const button of header.children) {
      button.className =
        "sb-bg-white sb-hover:bg-secondary-25 sb-black-50 sb-hover:black";
    }
  }

  setupButtons() {
    // Expand button
    const expandButton = document.getElementById("chat-room-expand-button");
    expandButton.addEventListener("click", () => this.expandOrCollapse());

    // Close button
    const closeButton = document.getElementById("chat-room-close-button");
    closeButton.addEventListener("click", () => this.closeChat());

    // Plus/Minus button
    const plusButton = document.getElementById("chat-room-plus-button");
    plusButton.addEventListener("click", () => this.toggleSecondary());
  }

  expandOrCollapse() {
    console.log("expandOrCollapse");
    const button = document.getElementById("chat-room-expand-button");

    if (this.expansionLevel === 0) {
      this.expansionLevel = 1;
      this.chatRoom.style.width = "80%";
      button.textContent = "<";
    } else if (this.expansionLevel === 1) {
      this.expansionLevel = 0;
      this.chatRoom.style.width = "30%";
      button.textContent = ">";
    }
    if (DEBUG) {
      console.log(`Expansion Level: ${this.expansionLevel}`);
      console.log(`Chat Room Width: ${this.chatRoom.style.width}`);
    }
  }

  closeChat() {
    console.log("Close Chat");
    this.chatRoom.style.transform = "translateX(-100%)";
    // Add your reopen button logic here
    this.addReopenButton();
  }

  addReopenButton() {
    const reopenButton = document.createElement("button");
    reopenButton.textContent = "Open Chat";
    reopenButton.style.transition = `all ${this.transitionDuration}s ${this.transitionStyle}`;
    reopenButton.className = `reopen-chat-button sb-black sb-border-primary sb-border-solid 
      sb-border-2 sb-rounded-full sb-px-4 sb-py-2
      sb-hover:border-secondary sb-hover:bg-secondary sb-hover:white`;
    setTimeout(() => {
      reopenButton.style.transform = "translateX(0%)";
    }, 100);

    reopenButton.addEventListener("click", () => {
      reopenButton.style.transform = "translateX(-110%)";
      this.chatRoom.style.transform = "translateX(0%)";
      setTimeout(() => {
        reopenButton.remove();
      }, this.transitionDuration * 1000);
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
  console.log(`Chat Room: ${event.target}`);
  if (event.target.id !== "chat-room") {
    return;
  }
  const chatRoom = new ChatRoom();
  console.log("Chat Room Created");
});
