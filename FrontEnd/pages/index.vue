<template>
  <v-row justify="center" dense>
    <v-row justify="center" dense>
      <v-col cols="12" md="6" v-for="listing in listings" :key="listing.id">
        <Listing
          :title="listing.title"
          :description="listing.description"
          :location="listing.location"
          :action="listing.action"
          :material="listing.material"
          :image="listing.image"
          :created-at="listing.created_at"
        />
      </v-col>
    </v-row>
  </v-row>
</template>

<script setup>
const listings = ref([]);

onMounted(async () => {
  try {
    const response = await fetch("http://localhost:5000");
    listings.value = response.json();
  } catch (error) {
    console.error(error);
  }
});
</script>
