<template>
  <v-app>
    <!-- Toolbar at the top of the screen -->
    <v-app-bar color="primary" height="48">
      <!-- Title of the application with adjusted margin and font size -->
      <v-app-bar-title class="text-h6 ms-3">
        <v-icon icon="mdi-apps"></v-icon>

        <span class="ms-1">My Application</span>
      </v-app-bar-title>
    </v-app-bar>

    <!-- Navigation drawer for menu actions -->
    <v-navigation-drawer v-model="drawer" temporary>
      <v-list>
        <!-- Menu items in the drawer with icons -->
        <v-list-item
          :to="{ name: 'index' }"
          title="Home"
          prepend-icon="mdi-home"
        ></v-list-item>

        <v-list-item
          :to="{ name: 'index' }"
          title="Products"
          prepend-icon="mdi-cube-outline"
        ></v-list-item>

        <v-list-item
          :to="{ name: 'index' }"
          title="Contact"
          prepend-icon="mdi-email"
        ></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Main content of the application -->
    <v-main>
      <slot />
    </v-main>

    <!-- Smaller footer at the bottom of the screen -->
    <v-footer app color="secondary" height="30">
      <v-container class="text-center text-caption">
        © {{ new Date().getFullYear() }} My Application - All Rights Reserved
      </v-container>
    </v-footer>
  </v-app>
</template>

<script setup>
const drawer = ref(false);
</script>
