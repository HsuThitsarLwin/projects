import { createApp } from 'vue'
import { createPinia } from "pinia";
import App from './App.vue'
import router from './router/index.js'
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import './assets/main.css'


/* import the fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'

/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

/* import specific icons */
import { faLock, faLink, faUserSecret,faShare, faEnvelope } from '@fortawesome/free-solid-svg-icons'


import vue3GoogleLogin from 'vue3-google-login'

import VueGoogleMaps from '@fawmi/vue-google-maps'


import { defineComponent } from 'vue'
import { GoogleMap, Marker } from 'vue3-google-map'


import VueEasyLightbox from 'vue-easy-lightbox'
import VueNumber from 'vue-number-animation'


export default defineComponent({
  components: { GoogleMap, Marker },
  setup() {
    const center = { lat: 40.689247, lng: -74.044502 }

    return { center }
  },

})


export function tConvert(time) {
  const timeString = time
  // Prepend any date. Use your birthday.
  const timeString12hr = new Date('1970-01-01T' + timeString + 'Z')
    .toLocaleTimeString('en-US',
      { timeZone: 'UTC', hour12: true, hour: 'numeric', minute: 'numeric' }
    );

  return timeString12hr
}

const pinia = createPinia()

/* add icons to the library */
library.add(faUserSecret, faLock, faLink, faShare, faEnvelope)

createApp(App)
.use(router).use(pinia)
.use(VueGoogleMaps, {
    load: {
        key: 'AIzaSyDCBtObBDUy_E5GwV4iWad9G7I3EhMNjt4'
    },
    autobindAllEvents: true,
    })
.use(vue3GoogleLogin, {
    clientId: '785352656664-clp2q5kst70jfde7lsivm0rm02gl84kk.apps.googleusercontent.com',
  })
.use(VueEasyLightbox)
.use(VueNumber)
.component('font-awesome-icon', FontAwesomeIcon)
.mount('#app')


