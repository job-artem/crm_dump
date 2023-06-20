<template>
  <v-text-field
    v-model="inputValue"
    :counter="counter"
    :dense="dense"
    :label="label"
    :maxlength="maxlength"
    :minlength="minlength"
    :outlined="outlined"
    :placeholder="placeholder"
    :rules="rules"
    :type="type"
  />
</template>

<script>
export default {
  name: 'input-ui',
  props: {
    label: {
      type: String,
      default: '',
    },
    rules: {
      type: Array,
      default: () => [],
    },
    placeholder: {
      type: String,
      default: '',
    },
    type: {
      type: String,
      default: 'text',
    },
    outlined: {
      type: Boolean,
      default: true,
    },
    dense: {
      type: Boolean,
      default: false,
    },
    counter: {
      type: [Boolean, Number, String],
      default: false,
    },
    maxlength: {
      type: Number,
      default: null,
    },
    minlength: {
      type: Number,
      default: null,
    },
    value: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      inputValue: this.value,
    };
  },
  watch: {
    value(newValue) {
      this.inputValue = newValue;
    },
  },
};
</script>
