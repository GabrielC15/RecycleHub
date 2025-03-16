<template>
  <v-sheet style="background-color: #00838f" width="100%" height="100%">
    <v-container>
      <v-row class="justify-center align-center">
        <v-col
          cols="auto"
          class="mt-5 d-flex flex-column justify-center align-center align-self-stretch"
          v-for="category in Categories"
          v-bind:key="category.title"
          style="width: 100px"
        >
          <v-btn :icon="category.icon" size="small" class="mt-0"></v-btn>
          <span
            class="mt-2 text-caption text-center d-flex flex-grow-1 align-center justify-center"
            style="
              width: 100px;
              white-space: normal;
              word-wrap: break-word;
              text-align: center;
            "
          >
            {{ category.title }}
          </span>
        </v-col>
      </v-row>

      <Listings />
    </v-container>
  </v-sheet>
</template>

<script setup>
const listings = ref([]);

const Categories = [
  { title: "Plastic", icon: "mdi-recycle" },
  { title: "Wood", icon: "mdi-tree" },
  { title: "Paper & Cardboard", icon: "mdi-file-document" },
  { title: "Metal", icon: "mdi-wrench" },
  { title: "Electronics", icon: "mdi-laptop" },
];

onMounted(async () => {
  try {
    const response = await fetch("http://localhost:5000");
    listings.value = response.json();
  } catch (error) {
    console.error(error);
  }
});
</script>
