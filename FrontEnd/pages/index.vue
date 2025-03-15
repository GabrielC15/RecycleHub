<template>
  <v-row justify="center" dense>
    <v-col cols="12" md="6">
      <Listing title="Product1"></Listing>
    </v-col>
    <v-col cols="12" md="6">
      <Listing title="Product2"></Listing>
    </v-col>
  </v-row>
</template>

<script setup>
const listings = ref([]);

onMounted(async () => {
  try {
    const response = await fetch("http://localhost:3000");
    listings.value = response.json();
  } catch (error) {
    console.error(error);
  }
});
</script>
