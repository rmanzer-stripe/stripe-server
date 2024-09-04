<template>
  <v-card>
    <v-expansion-panels flat>
      <v-expansion-panel>
        <v-expansion-panel-header>
          <v-card-title>Create Test Clock</v-card-title>

        </v-expansion-panel-header>
          <v-expansion-panel-content>
            <v-card-text>
              <v-form>
                <v-row justify="space-around">
                  <v-col cols="12" sm="12" md="5">
                    <v-text-field v-model="name" label="Name" hint="Enter a friendly name for this Test Clock" persistent-hint></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="12" md="5">
                    <v-menu
                      ref="menu"
                      v-model="menu"
                      :close-on-content-click="false"
                      :return_value.sync="date"
                      transition="scale-transition"
                      offset-y
                      min-width="auto"
                    >
                      <template v-slot:activator="{on, attrs}">
                        <v-text-field
                          v-model="date"
                          label="Select a frozen time. Will start a 00:00"
                          prepend-icon="mdi-calendar"
                          readonly
                          v-bind="attrs"
                          v-on="on"
                        ></v-text-field>
                      </template>
                      <v-date-picker v-model="date" no-title scrollable>
                        <v-spacer></v-spacer>
                        <v-btn text color="primary" @click="$refs.menu.save(date)">OK</v-btn>
                      </v-date-picker>
                    </v-menu>
                  </v-col>
                </v-row>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-row justify="center" class="my-5">
                <v-btn color="primary" :disabled="test_clock !== null" @click.prevent="createTestClock">
                  <v-icon left>
                    mdi-clock-alert-outline
                  </v-icon>
                  Create Test Clock
                </v-btn>
                <v-btn v-if="hasClock" icon @click="show = !show" >
                    <v-icon>{{ show ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
                  </v-btn>
              </v-row>
            </v-card-actions>
            <v-expand-transition>
              <div v-show="show">
                <v-divider></v-divider>
                <v-card-text>
                  <pre>{{ test_clock }}</pre>
                </v-card-text>
              </div>
            </v-expand-transition>
          </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-card>
</template>

<script>
export default {
  data: () =>({
    name: null,
    date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substring(0, 10),
    menu: false,
    show: false,
    test_clock: null
  }),
  computed: {
    timestamp() {
      return new Date(this.date).getTime() / 1000
    },
    hasClock() {
      return this.test_clock !== null
    }
  },
  methods: {
    async createTestClock() {
      const clock = await this.$axios.$post('/test_clocks/', {
        name: this.name,
        frozen_time: this.timestamp
      })
      this.test_clock = clock
    }
  }
}
</script>
