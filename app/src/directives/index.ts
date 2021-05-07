import { App } from 'vue'
import { tooltip } from '@/services/tooltip.service'

export default (app: App) => {

  app.directive('tooltip', {
    mounted: (el: HTMLElement, { value }) => {

      el.onmouseover = () => {
        tooltip().text(value)
        tooltip().show()
      }
      el.onmouseout = () => {
        tooltip().hide()
      }
    }
  })
}

