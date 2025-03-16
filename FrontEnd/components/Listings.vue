<template>
  <v-row justify="center" dense style="width: 100%">
    <v-col cols="12" md="6" lg="4">
      <Listing
        v-for="listing in listings"
        :key="listing.id"
        :listing="listing"
      />
    </v-col>
  </v-row>
</template>

<script setup>
import axios from "axios";
const listings = ref([]);

onMounted(async () => {
  try {
    const response = await axios.get("http://localhost:5000/listings");
    listings.value = response.data;
    console.log(listings.value);
  } catch (error) {
    console.error(error);
  }
});
</script>
