<template>
  <AppHeader v-if="state.section != 0" />

  <div id="tooltip"></div>

  <main ref="sectionsRef">
    <section class="flex flex-c">
      <div class="text-c">
        <h1>Expose your parliament</h1>
        <p>Der er meget snak om det politiske spil. Men hvad er det, politikerne rent faktisk siger og gør? Kom med bagom de store overskrifter og den enkle retorik, og se, hvad der egentlig fylder noget i Folketinget.</p>
        <button @click="state.section = 1" style="margin-top: 2rem">Let's expose them!</button>
      </div>
    </section>
    <section class="flex" style="background:white">
      <div class="flex-1 flex flex-c" style="background:#f9f9f9">
        <article>
          <h2>The network</h2>
          <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
        </article>
      </div>
      <div class="flex-1 flex flex-c">
        <Graph :data="miserables" />
      </div>
    </section>
    <section class="flex" style="background:white">
      <div class="flex-1 flex flex-c" style="background:#f9f9f9">
        <article>
          <h2>The distribution</h2>
          <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
        </article>
      </div>
      <div class="flex-1 flex flex-c">
        <Histogram :data="histogram"
          title="Degree distribution"
          xlabel="degree"
          ylabel="probability"
        />
      </div>
    </section>
    <section class="flex flex-c" style="background:var(--color-5)">
      <div class="text-c">
        <h1>Another section</h1>
        <img src="https://i.kym-cdn.com/entries/icons/original/000/006/707/nothing-to-do-here-template.jpg.scaled500.jpg" />
      </div>
    </section>
    <section class="flex flex-c" style="background:white">
      <div class="text-c">
        <p>A project by DTU Bachelor students Sam, Mikkel & Jonas</p>
        <br>
        <p><small>Based on publicly available data from</small></p>
        <img style="margin-right: 2rem" width="100" src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Seal_of_the_Folketing_of_Denmark.svg/1200px-Seal_of_the_Folketing_of_Denmark.svg.png" />
        <img width="100" src="https://media-exp1.licdn.com/dms/image/C4E0BAQHf8LUTijuRFA/company-logo_200_200/0/1617714850982?e=2159024400&v=beta&t=0tTCqR4sms7tZZ1UmiZQL1fnNTamthPK-JIDMIEqf1c" />
        <br><br><br>
        <p><small>Special thanks to</small></p>
        <p>Our teacher Laura who excellently pulled of an online course due to the circumstances</p>
      </div>
    </section>
  </main>
  <!--<router-view/>-->
</template>

<script lang="ts">
import { defineComponent, onBeforeMount, onMounted, reactive, ref, watch } from 'vue'
import router from '@/router'
import { useRouter, useRoute } from 'vue-router'

import AppHeader from '@/components/AppHeader.vue'
import Graph from '@/components/d3/Graph.vue'
import Histogram from '@/components/d3/Histogram.vue'

import miserables from '@/data/miserables'
import histogram from '@/data/histogram'

export default defineComponent({
  components: { AppHeader, Graph, Histogram },
  setup() {
    const state = reactive({
      section: 0
    })

    const sectionsRef = ref<HTMLElement | null>(null)
    const route = useRoute()

    onMounted(() => {
      let hasScrolled = false
      let sections = sectionsRef.value?.children || []
      document.addEventListener('wheel', e => {
      e.preventDefault()
      if (!hasScrolled) { 
        if (e.deltaY < 0 && state.section - 1 >= 0) {
          state.section--
        } else if (e.deltaY > 0 && state.section + 1 < sections.length) {
          state.section++
        }
      }
      hasScrolled = true
      setTimeout(() => {
          hasScrolled = false
      }, 500)
    }, {passive: false})
    })

    function scrollToSection(i: number) {
      const sections = sectionsRef.value?.children || []
      for (let section of sections) {
          section.classList.remove('active')
      }
      const next = sections[i]
      if (next) {
        next.classList.add('active')
        next.scrollIntoView({behavior: 'smooth'})
      }
    }

    watch(() => state.section, (next) => {
      scrollToSection(next)
      router.push('#s' + next)
    })

    watch(() => route.hash, (x) => {      
      const section = parseInt(x.split('#s')[1])
      state.section = section
    })

    return { state, sectionsRef, miserables, histogram }
  },
})
</script>


<style lang="scss">
@import '@/styles/main.scss';


section {
  h1,h2,h3,h4, p {
    opacity: 0;
    transform: translateY(-5rem);
    transition: all .5s .5s;
  }
  p {
    transition: all .5s .75s;
  }
}

section.active {
  h1,h2,h3,h4, p {
    opacity: 1;
    transform: translateY(0);
  }
}

</style>
