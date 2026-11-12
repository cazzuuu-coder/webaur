/* WEBAUR site configuration. This is the only file you need to edit for
   contact setup.

   CONTACT_EMAIL  — shown as a link in the footer and on the contact and
                    privacy pages. The contact form opens the visitor's own
                    email app with a prepared message to this address
                    (mailto), so nothing is sent until they press Send there.
                    The address is also written into the HTML by
                    _tools/build_pages.py (EMAIL); keep the two the same.
                    Leave empty to hide the address everywhere.

   FORMSPREE_ID   — optional Formspree form id, or a full
                    https://formspree.io/f/… URL. When set, the form is
                    sent through Formspree instead of opening an email app.
*/
window.WEBAUR_SITE = {
  CONTACT_EMAIL: "hello@webaur.com",
  FORMSPREE_ID: ""
};
