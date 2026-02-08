interface NewConversationBtnProps {
  onClick: () => void;
}

export default function NewConversationBtn({ onClick }: NewConversationBtnProps) {
  return (
    <button
      onClick={onClick}
      className="px-4 py-2 bg-white/20 backdrop-blur-sm text-white rounded-lg text-sm font-medium hover:bg-white/30 transition-all duration-200 border border-white/30 shadow-sm flex items-center"
    >
      <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
      </svg>
      New Chat
    </button>
  );
}