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
}
