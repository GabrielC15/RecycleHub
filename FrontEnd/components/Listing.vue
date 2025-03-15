<template>
  <v-container>
    <v-layout>
      <v-card hover>
        <v-card-title>
          <h2>{{ title }}</h2>
        </v-card-title>

        <v-card-text>
          line 1<br />
          line 2<br />
        </v-card-text>

        <v-card-actions>
          <v-btn color="success">Click #1</v-btn>
          <v-btn flat color="primary">Click #2</v-btn>
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
});
</script>
