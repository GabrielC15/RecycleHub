<template>
  <form>
    <v-text-field
      v-model="state.name"
      :counter="10"
      :error-messages="v$.name.$errors.map((e) => e.$message)"
      label="Title"
      required
      @blur="v$.name.$touch"
      @input="v$.name.$touch"
    ></v-text-field>

    <v-text-field
      v-model="state.description"
      :counter="10"
      :error-messages="v$.description.$errors.map((e) => e.$message)"
      label="Description"
      required
      @blur="v$.description.$touch"
      @input="v$.description.$touch"
    ></v-text-field>

    <v-select
      v-model="state.material"
      :error-messages="v$.material.$errors.map((e) => e.$message)"
      :items="materials"
      label="Material"
      required
      @blur="v$.material.$touch"
      @change="v$.material.$touch"
    ></v-select>

    <v-text-field
      v-model="state.location"
      :counter="10"
      :error-messages="v$.location.$errors.map((e) => e.$message)"
      label="Location"
      required
      @blur="v$.location.$touch"
      @input="v$.location.$touch"
    ></v-text-field>

    <v-text-field
      v-model="state.price"
      :counter="10"
      :error-messages="v$.price.$errors.map((e) => e.$message)"
      :precision="2"
      control-variant="hidden"
      label="Price"
      required
      @blur="v$.price.$touch"
      @input="v$.price.$touch"
    ></v-text-field>

    <v-select
      v-model="state.action"
      :error-messages="v$.action.$errors.map((e) => e.$message)"
      :items="actions"
      label="Action"
      required
      @blur="v$.action.$touch"
      @change="v$.action.$touch"
    ></v-select>

    <v-file-input
      v-model="state.image"
      :error-messages="v$.image.$errors.map((e) => e.$message)"
      show-size
      label="File input"
      accept="image/png, image/jpeg, image/jpg"
      prepend-icon="mdi-camera"
      @change="loadFile($event)"
    ></v-file-input>
    <v-img :src="fileUrl" height="100"></v-img>

    <v-btn class="me-4" @click="submitForm"> submit </v-btn>
  </form>
</template>

<script setup>
import { reactive, ref } from "vue";
import { useVuelidate } from "@vuelidate/core";
import { numeric, required } from "@vuelidate/validators";
import axios from "axios";

const initialState = {
  name: "",
  description: "",
  location: "",
  price: "",
  action: null,
  material: null,
};

const state = reactive({
  ...initialState,
});

const actions = ["Donate", "Sell"];
const materials = ["Wood", "Metal", "Paper", "Plastic", "Glass"];

const rules = {
  name: { required },
  description: { required },
  material: { required },
  location: { required },
  price: { required, numeric },
  action: { required },
  image: { required },
};

const v$ = useVuelidate(rules, state);

const file = ref(File);
const fileUrl = ref("");
const loadFile = (event) => {
  file.value = event.target.files[0];
  fileUrl.value = URL.createObjectURL(file.value);
  v$.value.image.$touch();
};

let token = "";
onMounted(() => {
  const instance = getCurrentInstance();
  if (import.meta.client) {
    const token = instance.proxy.$auth.strategy.token.getLocal();
    console.log("Token:", token);

    // Interceptor to add token automatically to every request
    axios.interceptors.request.use(
      (config) => {
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );
  }
});

// Function to submit the form
async function submitForm() {
  const result = await v$.value.$validate();
  if (result) {
    const formData = new FormData();
    formData.append("title", state.name);
    formData.append("description", state.description);
    formData.append("location", state.location);
    formData.append("action", state.action);
    formData.append("material", state.material);
    if (file.value) formData.append("image", file.value);

    try {
      const response = await axios.post(
        "http://localhost:5000/listings",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      console.log("Form submitted successfully:", response.data);
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  }
}
</script>
