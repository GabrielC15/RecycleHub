<template>
  <v-card hover max-width="400">
    <v-img :src="listing.image_url" height="250" cover></v-img>
    <v-card-title>
      <h2>{{ listing.title }}</h2>
    </v-card-title>

    <v-card-subtitle>
      {{ listing.price }}
    </v-card-subtitle>

    <v-card-actions>
      <v-btn color="success">{{ listing.action }}</v-btn>
      <v-btn flat color="primary">{{ listing.material }}</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>
defineProps({
  listing: Object,
});
</script>
