<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="bg">
      <q-toolbar>
        <q-btn flat dense round icon="menu" aria-label="Menu" @click="toggleLeftDrawer" />

        <q-toolbar-title>
          <div class="title-box">
            <a class="title" href="#/">
              Money-Manager
            </a>
          </div>
        </q-toolbar-title>

        <div>{{ appVersion }}</div>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" show-if-above bordered>
      <q-section>
        <q-item-label header>
          Pages
        </q-item-label>
        <LinkRoute v-for="link in linksListRoutes" :key="link.title" v-bind="link" />

      </q-section>

      <q-section>
        <q-list>
          <q-item-label header>
            Essential Links
          </q-item-label>
          <LinkExternal v-for="link in linksListExternal" :key="link.title" v-bind="link" />
        </q-list>
      </q-section>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<style>
.title-box {
  display: inline;
  background-color: rgba(253, 254, 252, 0);
  padding: 5px 5px;
  border-radius: 5px;
}

.title-box:hover {
  background-color: rgba(253, 254, 252, .25);
  transition: ease-in-out 0.25s;
}

.title {
  color: var(--white);
  text-decoration: none;
}



.bg {
  background-color: var(--secondary);
  color: var(--white);
}
</style>

<script setup>
import { ref } from 'vue'
import LinkExternal from 'components/LinkExternal.vue'
import LinkRoute from 'components/LinkRoute.vue'

defineOptions({
  name: 'MainLayout'
})

const linksListExternal = [
  {
    title: 'Github',
    caption: 'github.com/money-manager',
    icon: 'code',
    link: 'https://github.com/AndreGraca98/money-manager'
  },
  {
    title: 'Email',
    caption: 'andrepgraca@gmail.com',
    icon: 'email',
    link: 'mailto:andrepgraca@gmail.com'
  },
]

const linksListRoutes = [
  {
    title: 'Home',
    caption: 'Welcome to Money-Manager',
    icon: 'home',
    link: '#/'
  },
  {
    title: 'File Uploader',
    caption: 'Upload your files',
    icon: 'cloud_upload',
    link: '#/file-uploader'
  },
]

const leftDrawerOpen = ref(false)

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value
}

const appVersion = import.meta.env.VITE_APP_VERSION ? 'v' + import.meta.env.VITE_APP_VERSION : '' 
</script>
