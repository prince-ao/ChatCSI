document.addEventListener('DOMContentLoaded', () => {
  const chat_box = document.getElementById("chat-box");
  const send_button = document.getElementById('send-button')

  chat_box.addEventListener('input', (e) => {
    if (e.target.value == "") {
      send_button.disabled = true;
    } else {
      send_button.disabled = false;
    }
  })

  const observable = document.getElementById('messages')

  const scrollObserver = new MutationObserver(mutations => {
    for (let mutation of mutations) {
      if (mutation.type === 'childList') {
        observable.scrollTop = observable.scrollHeight;
      }
    }
  })

  const newNodeObserver = new MutationObserver(mutations => {
    mutations.forEach(mutation => {
      if (mutation.addedNodes.length) {
        mutation.addedNodes.forEach(newNode => {
          const pnode = newNode.children[1];
          if (pnode.classList.contains('typewriter')) {
            const text = pnode.innerHTML
            pnode.innerHTML = ''
            typewriterEffect(newNode.children[1], text, 10);
          }
        });
      }
    });
  });



  newNodeObserver.observe(observable, { childList: true });
  scrollObserver.observe(observable, { childList: true })
})

function get_textarea() {
  const textarea = document.getElementById("chat-box")
  const value = textarea.value

  add_user_input(value)

  textarea.value = ""

  return `${value}`
}

function add_user_input(message) {
  const holder = document.getElementById("test-dummy")

  holder.insertAdjacentHTML('beforebegin', `<div style="background-color: rgba(0, 0, 0, 0.0); margin-bottom: 20px;">
    <p style="font-weight: bold; margin-bottom: 0px;">You</p>
    <p style="margin-bottom: 0px;">${message}</p>
</div>`)


  holder.scrollIntoView({ behavior: 'smooth', block: 'end' });
}

function typewriterEffect(element, text, delay) {
  let i = 0;
  function typeWriter() {
    if (i < text.length) {
      let char = text.charAt(i);
      if (char === '<') {
        let tagEnd = text.indexOf('>', i);
        if (tagEnd !== -1) {
          element.innerHTML += text.slice(i, tagEnd + 1);
          i = tagEnd;
        }
      } else {
        element.innerHTML += char;
      }
      i++;
      element.scrollIntoView({ behavior: 'smooth', block: 'end' });
      setTimeout(typeWriter, delay);
    }
  }
  typeWriter();
}
