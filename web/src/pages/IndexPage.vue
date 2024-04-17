<template>

  <body>
    <q-page class="flex flex-center">
      <h1 style="color: black; font-size: 3em; text-align: center;">Welcome to Money-Manager</h1>
      <img src="~assets/money.png" style="width: 200px; height: 200px">
    </q-page>
  </body>
</template>

<style>
body {
  margin: 0;
  padding: 0;
  font-family: 'Arial', sans-serif;
  background: radial-gradient(#fdfefc, #f1a302, #3b4b72, #ed1c22);
  background-size: 400% 400%;
  animation: background_gradient 60s ease infinite;
}

@keyframes background_gradient {
  0% {
    background-position: left;
  }

  15% {
    background-position: 100% 0%;
  }

  25% {
    background-position: top;
  }

  40% {
    background-position: 0% 100%;
  }

  50% {
    background-position: right;
  }

  65% {
    background-position: 100% 100%;
  }

  75% {
    background-position: bottom;
  }

  90% {
    background-position: 0% 0%;
  }

  100% {
    background-position: left;
  }
}
</style>

<script setup>
defineOptions({
  name: 'IndexPage'
});
</script>
