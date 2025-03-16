<template>
  <v-card hover>
    <v-img :src="listing.image_url" height="200"></v-img>
    <v-card-title>
      <h2>{{ listing.title }}</h2>
    </v-card-title>

    <v-card-text>
      {{ listing.description }}
    </v-card-text>

    <v-card-actions>
      <v-btn color="success">{{ listing.action }}</v-btn>
      <v-btn flat color="primary">{{ listing.material }}</v-btn>
      <v-spacer></v-spacer>
      <v-btn icon><v-icon>bookmark</v-icon></v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>
defineProps({
  listing: Object,
});
</script>
