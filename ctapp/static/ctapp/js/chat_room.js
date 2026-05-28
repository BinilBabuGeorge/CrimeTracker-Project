(function () {
  function escapeHtml(value) {
    return String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function getCsrfToken() {
    var cookieValue = null;
    if (!document.cookie) {
      return cookieValue;
    }

    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i += 1) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, 10) === "csrftoken=") {
        cookieValue = decodeURIComponent(cookie.substring(10));
        break;
      }
    }
    return cookieValue;
  }

  window.initChatRoom = function initChatRoom(options) {
    var chatLog = document.getElementById(options.chatLogId);
    var chatInput = document.getElementById(options.inputId);
    var sendButton = document.getElementById(options.buttonId);
    var apiUrl = options.apiUrl;
    var emptyMessage = options.emptyMessage;
    var lastRenderedSignature = "";
    var pollHandle = null;

    function scrollChatToBottom() {
      chatLog.scrollTop = chatLog.scrollHeight;
    }

    function renderMessages(messages) {
      if (!messages.length) {
        chatLog.innerHTML = '<div class="text-center text-muted mt-5">' + escapeHtml(emptyMessage) + "</div>";
        lastRenderedSignature = "";
        return;
      }

      var signature = messages.map(function (item) {
        return item.message_id + ":" + item.message;
      }).join("|");

      if (signature === lastRenderedSignature) {
        return;
      }

      lastRenderedSignature = signature;
      chatLog.innerHTML = messages.map(function (item) {
        return (
          '<div class="msg-row ' + escapeHtml(item.sender_type) + '">' +
            '<div class="msg-bubble">' +
              '<div>' + escapeHtml(item.message) + "</div>" +
              '<div class="msg-meta">' + escapeHtml(item.time_label || item.created_at) + "</div>" +
            "</div>" +
          "</div>"
        );
      }).join("");

      scrollChatToBottom();
    }

    function refreshMessages() {
      return fetch(apiUrl, {
        method: "GET",
        headers: {
          "X-Requested-With": "XMLHttpRequest"
        },
        credentials: "same-origin"
      })
        .then(function (response) { return response.json(); })
        .then(function (data) {
          if (data.ok) {
            renderMessages(data.messages || []);
          }
        })
        .catch(function () {
          return null;
        });
    }

    function sendMessage() {
      var message = chatInput.value.trim();
      if (!message) {
        return;
      }

      fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
          "X-CSRFToken": getCsrfToken(),
          "X-Requested-With": "XMLHttpRequest"
        },
        body: "message=" + encodeURIComponent(message),
        credentials: "same-origin"
      })
        .then(function (response) { return response.json(); })
        .then(function (data) {
          if (data.ok) {
            chatInput.value = "";
            refreshMessages();
          }
        })
        .catch(function () {
          return null;
        });
    }

    sendButton.addEventListener("click", sendMessage);
    chatInput.addEventListener("keydown", function (event) {
      if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
      }
    });

    refreshMessages();
    pollHandle = window.setInterval(refreshMessages, options.pollMs || 2500);

    window.addEventListener("beforeunload", function () {
      if (pollHandle) {
        window.clearInterval(pollHandle);
      }
    });
  };
})();
