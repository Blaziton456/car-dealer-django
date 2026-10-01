import js from "@eslint/js";

export default [
    js.configs.recommended,
    {
        files: ["server/frontend/src/**/*.js", "server/frontend/src/**/*.jsx"],
        languageOptions: {
            ecmaVersion: 2022,
            sourceType: "module",
            parserOptions: {
                ecmaFeatures: {
                    jsx: true
                }
            },
            globals: {
                console: "readonly"
            }
        },
        rules: {
            "no-unused-vars": "off"
        }
    }
];