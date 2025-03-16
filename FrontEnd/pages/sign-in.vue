<template>
  <form class="d-flex flex-column">
    <v-text-field
      v-model="state.username"
      :counter="10"
      :error-messages="v$.username.$errors.map((e) => e.$message)"
      label="Name"
      required
      @blur="v$.username.$touch"
      @input="v$.username.$touch"
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

    <v-text-field
      v-model="state.password"
      :error-messages="v$.password.$errors.map((e) => e.$message)"
      :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
      :type="showPassword ? 'text' : 'password'"
      label="Password"
      @click:append="showPassword = !showPassword"
      @blur="v$.username.$touch"
      @input="v$.username.$touch"
    ></v-text-field>

    <v-btn-toggle divided variant="outlined" v-model="toggle" mandatory>
      <v-btn value="sign-up">Sign Up</v-btn>
      <v-btn value="log-in">Log In</v-btn>
    </v-btn-toggle>

    <v-btn class="me-4" @click="submitForm"> submit </v-btn>
  </form>
  <v-snackbar v-model="snackbar" timeout="1000">
    {{ signInMessage }}

    <template v-slot:actions>
      <v-btn color="blue" variant="text" @click="snackbar = false">
        Close
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script setup>
import { useVuelidate } from "@vuelidate/core";
import { required, email } from "@vuelidate/validators";
import axios from "axios";

const showPassword = ref(false);
const toggle = ref();
const snackbar = ref(false);
const state = reactive({
  name: "",
  email: "",
  password: "",
});
const v$ = useVuelidate(
  {
    username: { required },
    email: { email },
    password: { required },
  },
  state
);

const signInMessage = ref("");
const submitForm = async () => {
  const result = await v$.value.$validate();
  if (result) {
    if (toggle.value == "sign-up") {
      // Handle Sign Up
      try {
        const response = await axios.post("http://localhost:5000/signup", {
          username: state.username,
          email: state.email,
          password: state.password,
        });

        console.log("Sign up successful:", response.data);
      } catch (error) {
        if (error.response) {
          console.error("Sign up failed:", error.response.data);
        } else {
          console.error("Error during sign up:", error.message);
        }
      }
    } else if (toggle.value == "log-in") {
      // Handle Log In
      try {
        const response = await axios.post("http://localhost:5000/login", {
          username: state.username,
          password: state.password,
        });
        localStorage.setItem("access_token", response.data.access_token);

        console.log("Login successful:", response.data);
      } catch (error) {
        if (error.response) {
          console.error("Login failed:", error.response.data);
          alert(error.response.data.error);
        } else {
          console.error("Error during login:", error.message);
        }
      }
    }
  }
};
</script>
