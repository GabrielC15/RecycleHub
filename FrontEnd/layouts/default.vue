<template>
  <v-app>
    <!-- Toolbar at the top of the screen -->
    <v-app-bar style="background-color: #00838f" height="48">
      <!-- Title of the application with adjusted margin and font size -->
      <v-app-bar-title class="text-h6 ms-3">
        <v-icon icon="mdi-apps"></v-icon>

        <span class="ms-1">{{ appName }}</span>
      </v-app-bar-title>
    </v-app-bar>

    <!-- Navigation drawer for menu actions -->
    <v-navigation-drawer v-model="drawer" temporary>
      <v-list>
        <!-- Menu items in the drawer with icons -->
        <v-list-item
          :to="{ name: 'index' }"
          :title="menuItem1Title"
          prepend-icon="mdi-home"
        ></v-list-item>

        <v-list-item
          :to="{ name: 'index' }"
          :title="menuItem2Title"
          prepend-icon="mdi-cube-outline"
        ></v-list-item>

        <v-list-item
          :to="{ name: 'index' }"
          :title="menuItem3Title"
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
        {{ footerText }}
      </v-container>
    </v-footer>
  </v-app>
</template>

<script setup>
const drawer = ref(false);
const appName = "RecycleHub";
const menuItem1Title = "Home";
const menuItem2Title = "Products";
const menuItem3Title = "Contact";
const footerText = ` My Application - All Rights Reserved`;
</script>
