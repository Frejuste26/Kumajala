<template>
  <button
    :class="buttonClasses"
    :disabled="disabled || loading"
    @click="handleClick"
    @mouseenter="handleMouseEnter"
    @mouseleave="handleMouseLeave"
    :aria-label="ariaLabel"
    :type="type"
  >
    <!-- Icône de chargement -->
    <svg
      v-if="loading"
      class="loading-spinner"
      viewBox="0 0 24 24"
      width="16"
      height="16"
    >
      <circle
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        stroke-width="2"
        fill="none"
        stroke-linecap="round"
        stroke-dasharray="32"
        stroke-dashoffset="32"
      >
        <animate
          attributeName="stroke-dasharray"
          dur="2s"
          values="0 32;16 16;0 32;0 32"
          repeatCount="indefinite"
        />
        <animate
          attributeName="stroke-dashoffset"
          dur="2s"
          values="0;-16;-32;-32"
          repeatCount="indefinite"
        />
      </circle>
    </svg>

    <!-- Icône de gauche -->
    <component
      :is="leftIcon"
      v-if="leftIcon && !loading"
      class="button-icon left-icon"
    />

    <!-- Contenu du bouton -->
    <span
      v-if="!loading || showTextWhileLoading"
      class="button-content"
      :class="{ 'with-loading': loading && showTextWhileLoading }"
    >
      <slot>{{ text }}</slot>
    </span>

    <!-- Icône de droite -->
    <component
      :is="rightIcon"
      v-if="rightIcon && !loading"
      class="button-icon right-icon"
    />

    <!-- Effet de ripple -->
    <span
      v-if="ripple && rippleActive"
      class="ripple-effect"
      :style="rippleStyle"
    ></span>
  </button>
</template>

<script>
export default {
  name: 'GetStartedButton', 

  props: {
    // Variantes de style
    variant: {
      type: String,
      default: 'primary',
      validator: (value) => ['primary', 'secondary', 'tertiary', 'outline', 'ghost', 'danger'].includes(value)
    },

    // Tailles
    size: {
      type: String,
      default: 'md',
      validator: (value) => ['xs', 'sm', 'md', 'lg', 'xl'].includes(value)
    },

    // États
    disabled: {
      type: Boolean,
      default: false
    },

    loading: {
      type: Boolean,
      default: false
    },

    // Contenu
    text: {
      type: String,
      default: 'Get Started'
    },

    // Icônes (peut être un nom de composant ou un composant importé)
    leftIcon: {
      type: [String, Object],
      default: null
    },

    rightIcon: {
      type: [String, Object],
      default: null
    },

    // Options d'interaction
    ripple: {
      type: Boolean,
      default: true
    },

    showTextWhileLoading: {
      type: Boolean,
      default: false
    },

    // Attributs HTML
    type: {
      type: String,
      default: 'button'
    },

    ariaLabel: {
      type: String,
      default: null
    },

    // Styles personnalisés
    fullWidth: {
      type: Boolean,
      default: false
    },

    rounded: {
      type: String,
      default: 'md',
      validator: (value) => ['none', 'sm', 'md', 'lg', 'xl', 'full'].includes(value)
    }
  },

  emits: ['click', 'hover', 'blur'],

  data() {
    return {
      isHovered: false,
      rippleActive: false,
      rippleStyle: {}
    }
  },

  computed: {
    buttonClasses() {
      return [
        'enhanced-button',
        `variant-${this.variant}`,
        `size-${this.size}`,
        `rounded-${this.rounded}`,
        {
          'is-disabled': this.disabled,
          'is-loading': this.loading,
          'is-hovered': this.isHovered,
          'full-width': this.fullWidth,
          'has-left-icon': this.leftIcon,
          'has-right-icon': this.rightIcon
        }
      ]
    }
  },

  methods: {
    handleClick(event) {
      if (this.disabled || this.loading) return

      if (this.ripple) {
        this.createRipple(event)
      }

      this.$emit('click', event)
    },

    handleMouseEnter(event) {
      this.isHovered = true
      this.$emit('hover', { type: 'enter', event })
    },

    handleMouseLeave(event) {
      this.isHovered = false
      this.$emit('hover', { type: 'leave', event })
    },

    createRipple(event) {
      const button = event.currentTarget
      const rect = button.getBoundingClientRect()
      const size = Math.max(rect.width, rect.height)
      const x = event.clientX - rect.left - size / 2
      const y = event.clientY - rect.top - size / 2

      this.rippleStyle = {
        width: `${size}px`,
        height: `${size}px`,
        left: `${x}px`,
        top: `${y}px`
      }

      this.rippleActive = true

      setTimeout(() => {
        this.rippleActive = false
      }, 600)
    }
  }
}
</script>

<style scoped>
.enhanced-button {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  border: none;
  outline: none;
  font-family: var(--font-primary);
  font-weight: var(--fw-semibold);
  line-height: 1.5;
  cursor: pointer;
  user-select: none;
  text-decoration: none;
  overflow: hidden;
  white-space: nowrap;
  transition: all var(--transition-base),
              transform var(--transition-fast),
              box-shadow var(--transition-base);
  &:focus-visible {
    outline: 2px solid var(--cl-primary);
    outline-offset: 2px;
  }
  &:active {
    transform: translateY(1px) scale(0.98);
  }
}

.variant-primary {
  background: linear-gradient(135deg, var(--cl-primary) 0%, var(--cl-secondary) 100%);
  color: var(--cl-white);
  box-shadow: var(--shadow-sm);
  &:hover:not(.is-disabled):not(.is-loading) {
    background: linear-gradient(135deg, var(--cl-secondary) 0%, var(--cl-primary) 100%);
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
  }
}

.variant-secondary {
  background-color: var(--cl-secondary);
  color: var(--cl-white);
  box-shadow: var(--shadow-sm);
  &:hover:not(.is-disabled):not(.is-loading) {
    background-color: var(--cl-primary);
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
  }
}

.variant-tertiary {
  background-color: var(--cl-tertiary);
  color: var(--cl-white);
  box-shadow: var(--shadow-sm);
  &:hover:not(.is-disabled):not(.is-loading) {
    opacity: 0.9;
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
  }
}

.variant-outline {
  background-color: transparent;
  color: var(--cl-primary);
  border: 2px solid var(--cl-primary);
  &:hover:not(.is-disabled):not(.is-loading) {
    background-color: var(--cl-primary);
    color: var(--cl-white);
    transform: translateY(-1px);
  }
}

.variant-ghost {
  background-color: transparent;
  color: var(--cl-primary);
  &:hover:not(.is-disabled):not(.is-loading) {
    background-color: rgba(241, 137, 14, 0.1);
    transform: translateY(-1px);
  }
}

.variant-danger {
  background-color: var(--cl-error);
  color: var(--cl-white);
  &:hover:not(.is-disabled):not(.is-loading) {
    background-color: #dc2626;
    transform: translateY(-1px);
  }
}

.size-xs {
  padding: var(--space-1) var(--space-2);
  font-size: var(--fs-xs);
  min-height: 24px;
}

.size-sm {
  padding: var(--space-1) var(--space-3);
  font-size: var(--fs-sm);
  min-height: 32px;
}

.size-md {
  padding: var(--space-3) var(--space-6);
  font-size: var(--fs-base);
  min-height: 44px;
}

.size-lg {
  padding: var(--space-4) var(--space-8);
  font-size: var(--fs-lg);
  min-height: 52px;
}

.size-xl {
  padding: var(--space-5) var(--space-10);
  font-size: var(--fs-xl);
  min-height: 60px;
}

.rounded-none { border-radius: var(--radius-none); }
.rounded-sm { border-radius: var(--radius-sm); }
.rounded-md { border-radius: var(--radius-md); }
.rounded-lg { border-radius: var(--radius-lg); }
.rounded-xl { border-radius: var(--radius-xl); }
.rounded-full { border-radius: var(--radius-full); }

.is-disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}

.is-loading {
  cursor: wait;
}

.full-width {
  width: 100%;
}

.button-icon {
  flex-shrink: 0;
  width: 16px;
  height: 16px;
}

.size-xs .button-icon {
  width: 12px;
  height: 12px;
}

.size-sm .button-icon {
  width: 14px;
  height: 14px;
}

.size-lg .button-icon {
  width: 18px;
  height: 18px;
}

.size-xl .button-icon {
  width: 20px;
  height: 20px;
}

.button-content {
  transition: margin var(--transition-base);
}

.button-content.with-loading {
  margin-left: var(--space-1);
}

.loading-spinner {
  flex-shrink: 0;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.ripple-effect {
  position: absolute;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.3);
  pointer-events: none;
  animation: ripple-animation 0.6s ease-out;
}

@keyframes ripple-animation {
  0% {
    transform: scale(0);
    opacity: 1;
  }
  100% {
    transform: scale(1);
    opacity: 0;
  }
}

@media (max-width: 768px) {
  .enhanced-button {
    min-height: 48px;
  }

  .size-xs { min-height: 36px; }
  .size-sm { min-height: 40px; }
  .size-md { min-height: 48px; }
  .size-lg { min-height: 56px; }
  .size-xl { min-height: 64px; }
}

.enhanced-button {
  animation: fadeInUp 0.3s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (prefers-color-scheme: dark) {
  .variant-ghost:hover:not(.is-disabled):not(.is-loading) {
    background-color: rgba(241, 137, 14, 0.2);
  }

  .enhanced-button:focus-visible {
    outline-color: var(--cl-secondary);
  }
}

@media (prefers-reduced-motion: reduce) {
  .enhanced-button {
    transition: none;
    animation: none;
  }

  .loading-spinner {
    animation: none;
  }

  .ripple-effect {
    animation: none;
  }
}
</style>