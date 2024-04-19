<template>
    <q-page class="flex flex-center background-animation">
        <div class="box">
            <h1>About</h1>
            <p>
                This is a simple money manager application.
            </p>
            <p>
                The main goal is to help you get a better understanding of your finances, by
                providing a simple and easy to use interface to visualize your expenses and incomes.
            </p>
            <p>
                It is built using Quasar Framework and Vue.js.
                Connecting with an <a href="http://localhost:8100" target="_blank">API</a> built with FastAPI in
                <b>Python</b>.
            </p>
        </div>
    </q-page>
</template>

<style>
p {
    margin: 10px 0;
    color: var(--black);
}
</style>

<script setup>
defineOptions({
    name: "AboutPage",
});
</script>
