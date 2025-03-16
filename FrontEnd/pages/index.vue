<template>
  <v-sheet width="100%" height="100%" class="bg-teal-darken-3">
    <v-container class="d-flex flex-column align-center ma-10">
      <div class="text-h2 ma-5">RecycleHub</div>

      <v-text-field
        append-inner-icon="mdi-magnify"
        label="Search"
        style="width: 50%"
      ></v-text-field>

      <v-container class="d-flex justify-space-evenly">
        <v-btn append-icon="mdi-cart" to="/buy">Buy</v-btn>
        <v-btn append-icon="mdi-currency-usd" to="/sell">Sell</v-btn>
      </v-container>

      <h1>Categories</h1>
      <v-row class="d-flex justify-center align-center">
        <v-col
          cols="auto"
          class="mt-5 d-flex flex-column align-center align-self-stretch"
          v-for="category in Categories"
          v-bind:key="category.title"
        >
          <v-btn :icon="category.icon" size="small" class="mt-0"></v-btn>
          <span
            class="mt-2 text-caption text-center d-block"
            style="width: 100px"
            >{{ category.title }}</span
          >
        </v-col>
      </v-row>

      <Listings />
    </v-container>
  </v-sheet>
</template>

<script setup>
const Categories = ref([
  {
    title: "Plastic",
    icon: "mdi-home",
  },
  {
    title: "Wood",
    icon: "mdi-home",
  },
  {
    title: "Paper & Cardboard",
    icon: "mdi-home",
  },
  {
    title: "Metal",
    icon: "mdi-home",
  },
  {
    title: "Electronics",
    icon: "mdi-home",
  },
]);
</script>
