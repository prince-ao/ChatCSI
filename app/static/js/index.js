function get_textarea() {
  const textarea = document.getElementById("chat-box")
  const value = textarea.value

  textarea.value = ""

  return `${value}`
}
