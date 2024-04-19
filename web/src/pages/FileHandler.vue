<template>
    <q-page class="flex flex-center background-animation">
        <div class="box">
            <h1>File Handler</h1>

            <q-section>
                <q-item-label header>
                    List files
                </q-item-label>
                <!-- <q-btn @click="listFiles" color="primary" text-color="white">
                    List files
                </q-btn> -->
                {{ foo }}
                <q-list>
                    <q-item v-for="file in currentFiles" :key="file.id">
                        <q-item-section>
                            <q-item-label>{{ file.name }}</q-item-label>
                        </q-item-section>
                    </q-item>
                </q-list>
            </q-section>

            <q-section>
                <q-item-label header>
                    Upload a file
                </q-item-label>
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
import { api } from 'boot/axios';
defineOptions({
    name: "FileHandlerPage",
});

const currentFiles = api.get('storage?bucket_name=pdf')
    .then((response) => {
        response.data.files
    })
    .catch((error) => {
        []
    });

const foo = "bar"
</script>
