<template>
    <q-page class="flex flex-center background-animation">
        <div class="box ">
            <h1>File Uploader</h1>

            <q-uploader url="http://localhost:8100/storage/file"
                :headers="[{ 'accept': 'application/json', 'Content-Type': 'multipart/form-data' }]" :multiple="true"
                :auto-upload="false" :hide-upload-button="true" field-name="in_file">
                <!-- <template v-slot:header>
                    <q-btn flat label=" Select files" />
                </template> -->
            </q-uploader>
        </div>
    </q-page>
</template>

<style></style>

<script setup>
defineOptions({
    name: "FileUploader",
});


</script>
