document.addEventListener('mousemove', (e: MouseEvent) => {    
    tooltip().pos(e.clientX+20, e.clientY-20)
}, false)

export const tooltip = () => {
    const el = document.getElementById('tooltip')
    return {
        show () {
            el!.style.display = 'block'
        },
        hide () {
            el!.style.display = 'none'
        },
        text (value: string | number) {
            el!.innerHTML = value.toString()
        },
        pos (x: number, y: number) {
            el!.style.transform = `translate(${x}px, ${y}px)`
        }
    }
}