# Velvet Hour Audit - UI Component Specifications

## Buttons
- **Primary Button:**
  - Background: `#3A0CA3` (Velvet Primary)
  - Text: `#FFFFFF`
  - Border-radius: `8px`
  - Padding: `12px 24px`
  - Font: `Montserrat`, Bold, `16px`
  - Hover: Background `#7209B7` (Velvet Secondary), Transition `0.2s ease-in-out`.
- **CTA Button (High Conversion):**
  - Background: `#FFD700` (Gold Accent)
  - Text: `#212529` (Deep Slate)
  - Font-weight: `Bold`
  - Box-shadow: `0 4px 14px 0 rgba(255, 215, 0, 0.39)`
- **Secondary/Outline Button:**
  - Border: `2px solid #3A0CA3`
  - Text: `#3A0CA3`
  - Background: Transparent

## Cards
- **Audit Category Card:**
  - Background: `#FFFFFF`
  - Border-radius: `12px`
  - Padding: `20px`
  - Shadow: `0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)`
  - Header: Category name + score badge.
- **Fix Selection Card:**
  - Similar to Audit card but with a checkbox/toggle and a price tag in the bottom right.
  - Active state: Border `2px solid #FFD700`.

## Badges/Status Indicators
- **Score Badge:**
  - High (90-100): Background `#2ECC71` (Success Green), White text.
  - Med (70-89): Background `#F1C40F` (Yellow), Black text.
  - Low (<70): Background `#E63946` (Alert Red), White text.
- **Severity & Impact Tags:**
  - **Critical:** `-30` points. Tag: "Urgent — fix now". Color: Alert Red.
  - **High:** `-15` points. Tag: "Important — impacts revenue". Color: Dark Orange.
  - **Medium:** `-7` points. Tag: "Should fix". Color: Yellow.
  - **Low:** `-3` points. Tag: "Nice to have". Color: Blue.
  - **Info:** `0` points. Tag: "FYI". Color: Gray.

## Audit Categories & Weights
| Category | Weight |
|----------|--------|
| Mobile Responsiveness | 9% |
| Page Speed | 9% |
| SEO Fundamentals | 8% |
| Local SEO | 7% |
| Accessibility | 7% |
| User Experience | 7% |
| Navigation | 6% |
| Conversion Optimization | 8% |
| Calls to Action | 7% |
| Contact Visibility | 6% |
| Trust Signals | 6% |
| Reviews & Reputation | 4% |
| Content Quality | 5% |
| Image Optimization | 4% |
| Security Basics | 3% |
| Technical Issues | 2% |
| Lead Generation | 2% |

## Inputs
- **URL Input (Hero):**
  - Height: `56px`
  - Border-radius: `8px 0 0 8px` (if combined with button) or `8px` (standalone).
  - Font-size: `18px`
  - Placeholder color: `#ABB2BF`

## Navigation
- **Sidebar (Dashboard):**
  - Background: `#212529` (Deep Slate) or a very dark version of Velvet Primary.
  - Active Link: Left border `4px solid #FFD700`, Background `rgba(255, 255, 255, 0.05)`.

## Typography Scale (Base 16px)
- **H1:** `48px`, `Playfair Display`, Bold.
- **H2:** `36px`, `Playfair Display`, Semi-Bold.
- **H3:** `24px`, `Montserrat`, Bold.
- **Body:** `16px`, `Inter`, Regular.
- **Small:** `14px`, `Inter`, Regular.
