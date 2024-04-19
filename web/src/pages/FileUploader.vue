<template>
    <q-page class="flex flex-center background-animation">
        <div class="box">
            <h1>File Uploader</h1>
            <q-section>
                <q-uploader url="http://localhost:8100/storage/file" field-name="in_file"
                    :headers="[{ 'accept': 'application/json', 'Content-Type': 'multipart/form-data' }]"
                    :multiple="true" :auto-upload="false" :hide-upload-button="true" color="primary" text-color="white">
                </q-uploader>
            </q-section>

            <q-section>

            </q-section>
        </div>
    </q-page>
</template>

<style>
q-uploader {
    width: 100%;
    max-width: 400px;
    margin: 0 auto;

}
</style>

<script setup>
defineOptions({
    name: "FileUploaderPage",
});


</script>
