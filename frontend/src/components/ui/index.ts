// src/components/ui/index.ts
// Export only the main components (clean & tree-shake friendly)
export { Button } from './button';
import Input from './Input';
export { Input };
export {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
  // ← add any other Card* variants you actually use
} from './Card';
import Container from './Container';
export { Container };
import Grid from './Grid';
export { Grid };