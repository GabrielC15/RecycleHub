<template>
  <form>
    <v-text-field
      v-model="state.name"
      :counter="10"
      :error-messages="v$.name.$errors.map((e) => e.$message)"
      label="Name"
      required
      @blur="v$.name.$touch"
      @input="v$.name.$touch"
    ></v-text-field>

    <v-text-field
      v-if="toggle === 'sign-up'"
      v-model="state.email"
      :error-messages="v$.email.$errors.map((e) => e.$message)"
      label="E-mail"
      required
      @blur="v$.email.$touch"
      @input="v$.email.$touch"
    ></v-text-field>

    <v-btn-toggle v-model="toggle" mandatory>
      <v-btn icon="mdi-format-align-left" value="sign-up">Sign Up</v-btn>
      <v-btn icon="mdi-format-align-center" value="log-in">Log In</v-btn>
    </v-btn-toggle>

    <v-btn class="me-4" @click="submitForm"> submit </v-btn>
  </form>
</template>

<script setup>
import { useVuelidate } from "@vuelidate/core";
import { required, numeric } from "@vuelidate/validators";
import axios from "axios";

const state = reactive({
  name: "",
  description: "",
  location: "",
  price: "",
  action: null,
  material: null,
  file: null,
});

const v$ = useVuelidate(
  {
    name: { required },
    description: { required },
    location: { required },
    price: { required, numeric },
    action: { required },
    material: { required },
    file: {
      required: (value) => value instanceof File || "File is required",
    },
  },
  state
);

const fileUrl = ref("");

const handleFileUpload = (event) => {
  if (event) {
    state.file = event;
    fileUrl.value = URL.createObjectURL(event);
    v$.value.file.$touch();
  } else {
    state.file = null;
    fileUrl.value = "";
  }
};

const toggle = ref();
const submitForm = () => {
  if (toggle.value == "sign-up") {
    // Handle Sign Up
    axios
      .post("http://localhost:5000/signup", form.value)
      .then((response) => {
        console.log("User signed up successfully:", response.data);
      })
      .catch((error) => {
        console.error("Sign up error:", error.response.data);
      });
  } else if (toggle.value == "log-in") {
    // Handle Log In
    axios
      .post("http://localhost:5000/login", {
        username_or_email: form.value.username || form.value.email,
        password: form.value.password,
      })
      .then((response) => {
        const { access_token } = response.data;
        console.log("Login successful! Token:", access_token);
        localStorage.setItem("authToken", access_token); // Store token
      })
      .catch((error) => {
        console.error("Login error:", error.response.data);
      });
  }
};
</script>
