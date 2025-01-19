// chat_room.mjs
const DEBUG = true;
if (DEBUG) {
  console.log("Chat Room JS Initialized");
}

class ChatRoom {
  constructor() {
    this.isSecondaryOpen = false;
    this.transitionDuration = 0.25;
    this.transitionStyle = "ease-in-out";
    this.chatRoom = document.getElementById("chat-room");
    this.setupButtons();
    this.setupStyles();
    this.setupResizeHandle();
  }

  setupStyles() {
    this.chatRoom.style.transition = `all ${this.transitionDuration}s ${this.transitionStyle}`;

    this.chatRoom.style.width = "33%";
    const header = document.getElementById("chat-room-header");
    for (const button of header.children) {
      button.className =
        "sb-bg-white sb-hover:bg-secondary-25 sb-black-50 sb-hover:black sb-mr-2 sb-mt-1";
      if ((button.textContent === "-") | (button.textContent === "+")) {
        button.className += " sb-w-full";
      }
    }
  }

  setupButtons() {
    // Close button
    const closeButton = document.getElementById("chat-room-close-button");
    closeButton.addEventListener("click", () => this.closeChat());

    // Plus/Minus button
    const plusButton = document.getElementById("chat-room-plus-button");
    plusButton.addEventListener("click", () => this.toggleSecondary());

    // Settings button
    const settingsButton = document.getElementById("chat-room-settings-button");
    settingsButton.addEventListener("click", () =>
      this.toggleSettings(settingsButton)
    );
  }

  setupResizeHandle() {
    const handle = this.chatRoom.querySelector(".resize-handle");
    let isResizing = false;
    let startX, startWidth;

    handle.addEventListener("mousedown", (e) => {
      isResizing = true;
      startX = e.pageX;
      startWidth = this.chatRoom.offsetWidth;

      // Add temporary event listeners
      document.addEventListener("mousemove", handleMouseMove);
      document.addEventListener(
        "mouseup",
        () => {
          isResizing = false;
          document.removeEventListener("mousemove", handleMouseMove);
        },
        { once: true }
      );
    });

    const handleMouseMove = (e) => {
      if (!isResizing) return;

      const width = startWidth + (e.pageX - startX);
      // Convert to percentage of viewport width
      const widthPercentage = (width / window.innerWidth) * 100;

      // Limit the width between 20% and 95%
      const clampedWidth = Math.max(20, Math.min(95, widthPercentage));

      this.chatRoom.style.width = `${clampedWidth}%`;
    };
    const handleMouseUp = () => {
      isResizing = false;
      document.removeEventListener("mousemove", handleMouseMove);
      document.removeEventListener("mouseup", handleMouseUp);
      // Reset cursor
      document.body.style.cursor = "default";
    };

    handle.addEventListener("mousedown", (e) => {
      isResizing = true;
      startX = e.pageX;
      startWidth = this.chatRoom.offsetWidth;

      // Change cursor while dragging
      document.body.style.cursor = "ew-resize";

      document.addEventListener("mousemove", handleMouseMove);
      document.addEventListener("mouseup", handleMouseUp);

      // Prevent text selection while dragging
      e.preventDefault();
    });
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
      reopenButton.style.transform = "translateX(-120%)";
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
    this.styleButtonForToggle(button);
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

  toggleSettings(settingsButton) {
    console.log("Toggle Settings");
    const settingsDiv = document.getElementById("chat-settings");
    const messagesDiv = document.getElementById("chat-messages");
    if (settingsDiv.classList.contains("sb-hidden")) {
      settingsDiv.classList.remove("sb-hidden");
    } else {
      settingsDiv.classList.add("sb-hidden");
    }
    if (messagesDiv.classList.contains("sb-hidden")) {
      messagesDiv.classList.remove("sb-hidden");
    } else {
      messagesDiv.classList.add("sb-hidden");
    }
    this.styleButtonForToggle(settingsButton);
  }

  styleButtonForToggle(button) {
    if (button.classList.contains("sb-bg-white")) {
      button.classList.remove("sb-bg-white");
      button.classList.remove("sb-hover:bg-secondary-25");
      button.classList.add("sb-bg-primary-25");
      button.classList.add("sb-hover:bg-primary-25");
    } else {
      button.classList.remove("sb-bg-primary-25");
      button.classList.remove("sb-hover:bg-primary-25");
      button.classList.add("sb-bg-white");
      button.classList.add("sb-hover:bg-secondary-25");
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
