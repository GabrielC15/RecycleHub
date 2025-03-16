<template>
  <v-app>
    <!-- Toolbar at the top of the screen -->
    <v-app-bar color="teal-darken-3" height="48">
      <v-app-bar-nav-icon
        size="large"
        icon="mdi-menu"
        @click="drawer = !drawer"
        position="relative"
      />

      <!-- Spacer to push the following elements to the right -->
      <v-spacer />

      <!-- Menu icons on the right side of the toolbar -->
      <v-btn icon="mdi-cart" @click="navigateTo('/')"></v-btn>

      <v-btn
        append-icon="mdi-account-box"
        rounded
        @click="navigateTo('/products')"
        >Sign in</v-btn
      >

      <v-btn icon="mdi-logout" @click="navigateTo('/contact')"></v-btn>
    </v-app-bar>

    <!-- Navigation drawer for menu actions -->
    <v-navigation-drawer v-model="drawer" temporary>
      <v-list>
        <!-- Menu items in the drawer with icons -->
        <v-list-item
          @click="navigateTo('/index')"
          title="Home"
          prepend-icon="mdi-home"
        ></v-list-item>

        <v-list-item
          @click="navigateTo('/products')"
          title="Products"
          prepend-icon="mdi-cube-outline"
        ></v-list-item>

        <v-list-item
          @click="navigateTo('/contact')"
          title="Contact"
          prepend-icon="mdi-email"
        ></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Main content of the application -->
    <v-main class="layout">
      <NuxtPage />
    </v-main>

    <!-- Smaller footer at the bottom of the screen -->
    <v-footer app color="secondary" height="30">
      <v-container class="text-caption text-center">
        © {{ new Date().getFullYear() }} My Application - All Rights Reserved
      </v-container>
    </v-footer>
  </v-app>
</template>

<script setup>
// Drawer state to open/close the navigation drawer
const drawer = shallowRef(false);
</script>
