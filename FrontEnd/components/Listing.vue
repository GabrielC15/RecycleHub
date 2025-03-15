<template>
  <v-container>
    <v-layout>
      <v-card hover>
        <v-img :src="{ image }"></v-img>
        <v-card-title>
          <h2>{{ title }}</h2>
        </v-card-title>

        <v-card-text>
          {{ description }}
        </v-card-text>

        <v-card-actions>
          <v-btn color="success">{{ action }}</v-btn>
          <v-btn flat color="primary">{{ material }}</v-btn>
          <v-spacer></v-spacer>
          <v-btn icon><v-icon>bookmark</v-icon></v-btn>
        </v-card-actions>
      </v-card>
    </v-layout>
  </v-container>
</template>

<script setup>
defineProps({
  title: String,
  description: String,
  location: String,
  action: String,
  material: String,
  image: String,
  createdAt: Date,
});
</script>
