export default function ErrorMessage({ message, onRetry }) {
  return (
    <div className="message-card error-card" role="alert">
      <span className="message-icon" aria-hidden="true">!</span>
      <div>
        <strong>We couldn’t load this information</strong>
        <p>{message}</p>
        {onRetry && <button className="text-button" onClick={onRetry}>Try again</button>}
      </div>
    </div>
  );
}
