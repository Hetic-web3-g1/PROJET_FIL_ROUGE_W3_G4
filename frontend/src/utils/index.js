export const setStore = (name, content) => {
    if (!name) return
    if (typeof content !== 'string') {
      content = JSON.stringify(content)
    }
    return window.localStorage.setItem(name, content)
  }
  
export const getStore = (name) => {
    if (!name) return
    return JSON.parse(window.localStorage.getItem(name))
}